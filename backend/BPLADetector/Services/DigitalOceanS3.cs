using BPLADetector.Application.Abstractions;
using BPLADetector.Application.DTO;
using BPLADetector.Configuration;
using BPLADetector.Constants;
using BPLADetector.Domain.Enums;
using BPLADetector.Domain.Helpers;
using Microsoft.Extensions.Options;

namespace BPLADetector.Services;

public class DigitalOceanS3 : S3Service, IS3Service
{
    private readonly DigitalOceanOptions _options;
    private readonly ILogger<DigitalOceanS3> _logger;

    public DigitalOceanS3(
        IOptions<DigitalOceanOptions> options,
        ILogger<DigitalOceanS3> logger) : base(options.Value.AccessKey,
        options.Value.SecretKey,
        options.Value.Endpoint)
    {
        _logger = logger;
        _options = options.Value;
    }

    public async Task<List<UploadedFileDto>> PutObjectsAsync(
        IEnumerable<UploadFileItem> files,
        CancellationToken cancellationToken = default)
    {
        var utcNow = DateTime.UtcNow;

        var uploadedFiles = new List<UploadedFileDto>();

        foreach (var file in files)
        {
            var key = GetKey(utcNow, file.Filename);

            if (file.Length > 90_000_000)
            {
                await MultiPartUploadAsync(
                    file.Stream, 
                    key, 
                    DigitalOceanConsts.DigitalOceanBucketName,
                    cancellationToken);
            }
            else
            {
                await PutObjectAsync(
                    file.Stream,
                    key,
                    DigitalOceanConsts.DigitalOceanBucketName,
                    cancellationToken);
            }

            var presignedUrl = GetFileUri(key).ToString();
            uploadedFiles.Add(new UploadedFileDto
            {
                UploadDatetime = utcNow,
                Filename = file.Filename,
                OriginalPresignedUrl = presignedUrl,
                Uri = presignedUrl,
                Status = UploadStatus.InProgress,
                Type = FileTypeHelper.GetFileType(file.Filename)
            });

            _logger.LogInformation($"Presigned uri for file {key}: {presignedUrl}");
        }

        return uploadedFiles;
    }

    private Uri GetFileUri(string key)
    {
        var baseUri = new Uri(
            _options.Endpoint.Replace("https://", $"https://{DigitalOceanConsts.DigitalOceanBucketName}."));

        return new Uri(baseUri, key);
    }
}