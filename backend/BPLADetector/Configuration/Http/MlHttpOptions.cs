namespace BPLADetector.Configuration.Http;

public class MlHttpOptions : IBaseOptions
{
    public static string Section => "MlHttp";

    public string BaseUri { get; set; }
}