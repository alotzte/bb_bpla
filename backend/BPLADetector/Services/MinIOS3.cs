using Amazon.S3.Model;
using BPLADetector.Application.Abstractions;
using BPLADetector.Application.DTO;
using BPLADetector.Configuration;
using BPLADetector.Constants;
using BPLADetector.Domain.Enums;
using BPLADetector.Domain.Helpers;
using Microsoft.Extensions.Options;

namespace BPLADetector.Services;

public class MinIOS3 : S3Service, IS3Service
{
    private readonly MinIOOptions _options;
    private readonly ILogger<MinIOS3> _logger;

    public MinIOS3(
        IOptions<MinIOOptions> options,
        ILogger<MinIOS3> logger) : base(
        logger,
        options.Value.AccessKey,
        options.Value.SecretKey,
        options.Value.Endpoint)
    {
        _options = options.Value;
        _logger = logger;
    }

    public async Task<List<UploadedFileDto>> PutObjectsAsync(
        IEnumerable<UploadFileItem> files,
        CancellationToken cancellationToken = default)
    {
        var utcNow = DateTime.UtcNow;

        var uploadedFiles = new List<UploadedFileDto>();

        _logger.LogInformation($"Received files: {string.Join(",", files.Select(file => file.Filename))}");

        await CreateBucketIfNotExists(MinIOConsts.BucketName, cancellationToken);

        foreach (var file in files)
        {
            var key = GetKey(utcNow, file.Filename);

            await PutObjectAsync(
                file.Stream,
                key,
                MinIOConsts.BucketName,
                cancellationToken);

            var presignedUrl = await GetPresignedUrlAsync(key, DateTime.Now.AddDays(14));
            _logger.LogInformation("=====\nOriginal presigned URL: {presignedUrl}\n=====", presignedUrl);

            uploadedFiles.Add(new UploadedFileDto
            {
                UploadDatetime = utcNow,
                Filename = file.Filename,
                OriginalPresignedUrl = presignedUrl,
                Uri = TransformPresignedUrl(presignedUrl),
                Status = UploadStatus.Processed,
                Type = FileTypeHelper.GetFileType(file.Filename)
            });
        }

        return uploadedFiles;
    }

    public async Task<string> GetPresignedUrlAsync(
        string key,
        DateTime? expires,
        string bucketName = MinIOConsts.BucketName)
    {
        var presignedUrlRequest = new GetPreSignedUrlRequest
        {
            BucketName = bucketName,
            Key = key,
            Expires = expires ?? DateTime.Now.AddDays(14)
        };

        var presignedUrl = await _client.GetPreSignedURLAsync(presignedUrlRequest);

        if (presignedUrl.Contains("https:"))
        {
            presignedUrl = presignedUrl!.Replace("https:", "http:");
        }

        return presignedUrl;
    }

    public string TransformPresignedUrl(string presignedUrl)
    {
        if (_options.NeedTransformUrl is false)
        {
            return presignedUrl;
        }

        if (presignedUrl.Contains("https:"))
        {
            presignedUrl = presignedUrl!.Replace("https:", "http:");
        }

        if (_options.MinioServiceHostname is not null && presignedUrl.Contains(_options.MinioServiceHostname))
        {
            presignedUrl = presignedUrl!.Replace(_options.MinioServiceHostname, _options.MinioHostname);
        }

        if (_options.MinioServicePort is not null && presignedUrl.Contains(_options.MinioServicePort))
        {
            presignedUrl = presignedUrl!.Replace(_options.MinioServicePort, _options.MinioPort);
        }

        return presignedUrl;
    }
}