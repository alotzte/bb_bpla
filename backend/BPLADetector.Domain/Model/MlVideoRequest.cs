using System.Text.Json.Serialization;

namespace BPLADetector.Domain.Model;

public class MlVideoRequest
{
    [JsonPropertyName("urls")] public string[] Urls { get; set; }
}