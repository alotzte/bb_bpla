using Amazon.Runtime;
using Amazon.S3;
using Amazon.S3.Model;
using Amazon.S3.Transfer;

namespace BPLADetector.Services;

public abstract class S3Service : IDisposable
{
    private readonly AmazonS3Client _client;

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

    private async Task<ListBucketsResponse> ListBucketsAsync(CancellationToken cancellationToken = default)
    {
        return await _client.ListBucketsAsync(cancellationToken);
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