using BPLADetector.Domain.Model;

namespace BPLADetector.Application.Handlers.File.GetProcessedFile;

public sealed class GetProcessedFileResponse
{
    public string Link { get; set; }
    public float[]? Marks { get; set; }
    public string Type { get; set; }

    public static GetProcessedFileResponse FromProcessedFile(ProcessedFile file)
    {
        return new GetProcessedFileResponse
        {
            Link = file.Uri,
            Marks = file.Marks ?? null,
            Type = file.Type.ToString().ToLower()
        };
    }
}