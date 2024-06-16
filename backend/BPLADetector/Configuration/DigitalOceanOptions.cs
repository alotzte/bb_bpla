namespace BPLADetector.Configuration;

public class DigitalOceanOptions : IBaseOptions
{
    public static string Section => "DigitalOcean";

    public string AccessKey { get; set; }
    public string SecretKey { get; set; }
    public string Endpoint { get; set; }
}