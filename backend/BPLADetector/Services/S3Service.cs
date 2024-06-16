using Amazon.Runtime;
using Amazon.S3;
using Amazon.S3.Model;
using Amazon.S3.Transfer;
using BPLADetector.Constants;

namespace BPLADetector.Services;

public abstract class S3Service : IDisposable
{
    protected readonly AmazonS3Client _client;

    protected S3Service(string accessKey, string secretKey, string endpoint)
    {
        _client = new AmazonS3Client(
            new BasicAWSCredentials(accessKey, secretKey),
            new AmazonS3Config
            {
                ForcePathStyle = true, 
                ServiceURL = endpoint
            });
    }

    public async Task<ListBucketsResponse> ListBucketsAsync(CancellationToken cancellationToken = default)
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
        string key,
        string bucketName,
        Stream fileStream,
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

    public void Dispose() => _client.Dispose();
}