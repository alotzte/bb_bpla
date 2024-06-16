namespace BPLADetector.Configuration;

public class CloudOptions : IBaseOptions
{
    public static string Section => "S3";

    public required string TenantId { get; init; }
    public required string KeyId { get; init; }
    public required string KeySecret { get; init; }
    public required string Endpoint { get; init; }
}