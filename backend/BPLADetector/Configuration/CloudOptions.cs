namespace BPLADetector.Configuration;

public class CloudOptions : IBaseS3Options
{
    public static string Section => "S3";
    public bool NeedTransformUrl { get; set; } = false;

    public required string TenantId { get; init; }
    public required string KeyId { get; init; }
    public required string KeySecret { get; init; }
    public required string Endpoint { get; init; }
}