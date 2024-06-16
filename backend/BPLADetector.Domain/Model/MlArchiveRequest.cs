using System.Text.Json.Serialization;

namespace BPLADetector.Domain.Model;

public class MlArchiveRequest
{
    [JsonPropertyName("archives")] public ArchiveItem[] Archives { get; set; }

    public class ArchiveItem
    {
        [JsonPropertyName("url")] public string Url { get; set; }
        [JsonPropertyName("correlation_id")] public Guid CorrelationId { get; set; }
    }
}