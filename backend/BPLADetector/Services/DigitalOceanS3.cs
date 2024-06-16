using BPLADetector.Application.Abstractions;
using BPLADetector.Application.DTO;
using BPLADetector.Configuration;
using BPLADetector.Constants;
using BPLADetector.Domain.Enums;
using BPLADetector.Domain.Helpers;
using BPLADetector.Domain.Model;
using Microsoft.Extensions.Options;

namespace BPLADetector.Services;

public class DigitalOceanS3 : S3Service, IS3Service
{
    private readonly DigitalOceanOptions _options;
    private readonly ILogger<DigitalOceanS3> _logger;
    private readonly IDomainRepository _domainRepository;

    public DigitalOceanS3(
        IOptions<DigitalOceanOptions> options,
        ILogger<DigitalOceanS3> logger,
        IDomainRepository domainRepository) : base(
        logger,
        options.Value.AccessKey,
        options.Value.SecretKey,
        options.Value.Endpoint)
    {
        _logger = logger;
        _domainRepository = domainRepository;
        _options = options.Value;
    }

    public async Task<List<UploadedFile>> PutObjectsAsync(
        IEnumerable<UploadFileItem> files,
        CancellationToken cancellationToken = default)
    {
        var utcNow = DateTime.UtcNow;

        var uploadedFiles = new List<UploadedFile>();

        foreach (var file in files)
        {
            var key = GetKey(utcNow, file.Filename);

            await PutObjectAsync(
                file.Stream,
                key,
                DigitalOceanConsts.DigitalOceanBucketName,
                cancellationToken);

            uploadedFiles.Add(new UploadedFile
            {
                UploadDatetime = utcNow,
                Filename = file.Filename,
                Uri = GetFileUri(key).ToString(),
                Status = UploadStatus.Processed,
                Type = FileTypeHelper.GetFileType(file.Filename)
            });

            _logger.LogInformation("Uri: {key}", GetFileUri(key));
        }

        return uploadedFiles;
    }

    public async Task MultiPartUploadAsync(
        string fileName,
        Stream fileStream,
        CancellationToken cancellationToken = default)
    {
        var utcNow = DateTime.UtcNow;
        var key = GetKey(utcNow, fileName);

        await base.MultiPartUploadAsync(
            key,
            DigitalOceanConsts.DigitalOceanBucketName,
            fileStream,
            cancellationToken);

        var uri = GetFileUri(key);
        _logger.LogInformation("Uri: {key}", uri);

        await _domainRepository.AddAsync(new UploadedFile
        {
            UploadDatetime = utcNow,
            Filename = fileName,
            Uri = uri.ToString(),
            Status = UploadStatus.Ready,
            Type = FileTypeHelper.GetFileType(fileName)
        }, cancellationToken);
        await _domainRepository.SaveChangesAsync(cancellationToken);
    }

    private Uri GetFileUri(string key)
    {
        var baseUri = new Uri(
            _options.Endpoint.Replace("https://", $"https://{DigitalOceanConsts.DigitalOceanBucketName}."));

        return new Uri(baseUri, key);
    }
}