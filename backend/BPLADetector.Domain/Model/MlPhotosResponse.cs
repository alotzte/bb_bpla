using System.Text.Json.Serialization;

namespace BPLADetector.Domain.Model;

public sealed class MlPhotosResponse
{
    public string Type { get; set; }
    [JsonPropertyName("predicted_data")] public List<PredictedDataPhoto> PredictedData { get; set; }
}

public sealed class PredictedDataPhoto
{
    [JsonPropertyName("link")] public string Link { get; set; }
    [JsonPropertyName("txt_path")] public string TxtPath { get; set; }
    [JsonPropertyName("correlation_id")] public Guid CorrelationId { get; set; }
}