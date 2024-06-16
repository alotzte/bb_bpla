using System.Net;
using Amazon.S3;
using Amazon.S3.Model;
using BPLADetector.Application.Abstractions;
using BPLADetector.Application.DTO;
using BPLADetector.Configuration;
using BPLADetector.Constants;
using BPLADetector.Domain.Enums;
using BPLADetector.Domain.Model;
using Microsoft.Extensions.Options;

namespace BPLADetector.Services;

public class MinIOS3 : S3Service, IS3Service
{
    private readonly MinIOOptions _options;
    private readonly ILogger<MinIOS3> _logger;
    private readonly IDomainRepository _domainRepository;

    public MinIOS3(
        IOptions<MinIOOptions> options,
        ILogger<MinIOS3> logger,
        IDomainRepository domainRepository) : base(
        options.Value.AccessKey,
        options.Value.SecretKey,
        options.Value.Endpoint)
    {
        _options = options.Value;
        _logger = logger;
        _domainRepository = domainRepository;
    }

    public async Task<List<UploadedFile>> PutObjectsAsync(
        IEnumerable<UploadFileItem> files,
        CancellationToken cancellationToken = default)
    {
        var utcNow = DateTime.UtcNow;

        var uploadedFiles = new List<UploadedFile>();

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
            _logger.LogInformation("=====\nPresigned URL: {presignedUrl}\n=====", presignedUrl);
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
        presignedUrl = presignedUrl!.Replace("https:", "http:");
        presignedUrl = presignedUrl!.Replace(_options.MinioServiceHostname, _options.MinioHostname);
        presignedUrl = presignedUrl!.Replace(_options.MinioServicePort, _options.MinioPort);

        return presignedUrl;
    }

    private async Task CreateBucketIfNotExists(string bucketName, CancellationToken cancellationToken = default)
    {
        _logger.LogInformation($"Try request bucket list");
        
        var buckets = await _client.ListBucketsAsync(cancellationToken);
        
        if (buckets.Buckets.Select(bucket => bucket.BucketName).Contains(bucketName))
        {
            _logger.LogInformation($"Bucket {bucketName} already exists");
            return;
        }
        
        _logger.LogInformation($"Trying create bucket {bucketName}");
        var putBucketRequest = new PutBucketRequest
        {
            CannedACL = S3CannedACL.PublicReadWrite,
            BucketName = bucketName
        };

        var putBucketResponse = await _client.PutBucketAsync(putBucketRequest, cancellationToken);

        if (putBucketResponse.HttpStatusCode != HttpStatusCode.OK)
        {
            throw new ApplicationException($"Не удалось создать bucket: {bucketName}");
        }
        
        _logger.LogInformation($"Bucket {bucketName} sucessfully created");
    }

    private static string GetPrefix(DateTime dateTime)
    {
        return dateTime.ToString("yyyyMMdd_hhmmss");
    }

    private static string GetKey(DateTime dateTime, string filename)
    {
        return $"{GetPrefix(dateTime)}/{filename}";
    }

    private Uri GetFileUri(string key)
    {
        var baseUri = new Uri(
            _options.Endpoint.Replace("https://", $"https://{DigitalOceanConsts.DigitalOceanBucketName}."));

        return new Uri(baseUri, key);
    }

    private static FileType GetFileType(string filename)
    {
        var extension = Path.GetExtension(filename).Replace(".", string.Empty);

        return extension switch
        {
            "jpg" or "png" or "psd" or "jpeg" => FileType.Image,
            "mp4" or "avi" or "mov" or "wmv" or "m4v" or "webm" => FileType.Video,
            // TODO: заменить на тип архив
            "zip" or "tar" or "rar" => FileType.Archive,
            _ => throw new ArgumentOutOfRangeException()
        };
    }
}