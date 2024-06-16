namespace BPLADetector.Configuration;

public class DigitalOceanOptions : IBaseS3Options
{
    public static string Section => "DigitalOcean";
    public bool NeedTransformUrl { get; set; } = false;

    public string AccessKey { get; set; }
    public string SecretKey { get; set; }
    public string Endpoint { get; set; }
}