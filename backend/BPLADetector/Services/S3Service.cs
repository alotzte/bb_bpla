using System.Net;
using Amazon.Runtime;
using Amazon.S3;
using Amazon.S3.Model;
using Amazon.S3.Transfer;
using BPLADetector.Constants;

namespace BPLADetector.Services;

public abstract class S3Service : IDisposable
{
    private readonly ILogger _logger;
    protected readonly AmazonS3Client _client;

    protected S3Service(ILogger logger, string accessKey, string secretKey, string endpoint)
    {
        _logger = logger;
        _client = new AmazonS3Client(
            new BasicAWSCredentials(accessKey, secretKey),
            new AmazonS3Config
            {
                ForcePathStyle = true, 
                ServiceURL = endpoint
            });
    }

    private async Task<ListBucketsResponse> ListBucketsAsync(CancellationToken cancellationToken = default)
    {
        return await _client.ListBucketsAsync(cancellationToken);
    }

    public async Task<List<S3Object>> ListObjectsV2(CancellationToken cancellationToken = default)
    {
        var request = new ListObjectsV2Request()
        {
            BucketName = DigitalOceanConsts.DigitalOceanBucketName,
            MaxKeys = 5
        };

        var responseObjects = new List<S3Object>();
        ListObjectsV2Response response;
        do
        {
            response = await _client.ListObjectsV2Async(request, cancellationToken);

            responseObjects.AddRange(response.S3Objects);

            request.ContinuationToken = response.NextContinuationToken;
        } while (response.IsTruncated);

        return responseObjects;
    }

    protected Task<PutObjectResponse> PutObjectAsync(
        Stream fileStream,
        string key,
        string bucketName,
        CancellationToken cancellationToken = default)
    {
        var putObjectRequest = new PutObjectRequest
        {
            BucketName = bucketName,
            Key = key,
            InputStream = fileStream,
            CannedACL = S3CannedACL.PublicRead
        };

        return _client.PutObjectAsync(putObjectRequest, cancellationToken);
    }

    protected async Task MultiPartUploadAsync(
        Stream fileStream,
        string key,
        string bucketName,
        CancellationToken cancellationToken = default)
    {
        var fileTransferUtility = new TransferUtility(_client);

        var request = new TransferUtilityUploadRequest
        {
            BucketName = bucketName,
            Key = key,
            InputStream = fileStream,
            CannedACL = S3CannedACL.PublicRead,
            AutoCloseStream = true
        };

        await fileTransferUtility.UploadAsync(request, cancellationToken);
    }

    protected async Task CreateBucketIfNotExists(string bucketName, CancellationToken cancellationToken = default)
    {
        _logger.LogInformation($"Try request bucket list");
        
        var buckets = await ListBucketsAsync(cancellationToken);
        
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
    
    private static string GetFolderPrefix(DateTime dateTime)
    {
        return dateTime.ToString("yyyyMMdd_hhmmss");
    }
    protected static string GetKey(DateTime dateTime, string filename)
    {
        return $"{GetFolderPrefix(dateTime)}/{filename}";
    }

    public void Dispose() => _client.Dispose();
}