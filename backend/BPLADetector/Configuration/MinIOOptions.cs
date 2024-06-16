namespace BPLADetector.Configuration;

public class MinIOOptions : IBaseS3Options
{
    public static string Section => "MinIO";
    public bool NeedTransformUrl { get; set; } = true;

    public string? MinioServiceHostname { get; set; }
    public string? MinioServicePort { get; set; }
    public string? MinioHostname { get; set; }
    public string? MinioPort { get; set; }
    public string AccessKey { get; set; }
    public string SecretKey { get; set; }
    public string Endpoint { get; set; }
}