using System.Runtime.InteropServices.ComTypes;
using BPLADetector.Domain.Enums;

namespace BPLADetector.Domain.Model;

public class UploadedFile
{
    public int Id { get; set; }
    public DateTime UploadDatetime { get; set; }
    public string Filename { get; set; } = null!;
    public string Uri { get; set; } = null!;
    public FileType Type { get; set; }
    public UploadStatus Status { get; set; }
    public Guid CorrelationId { get; set; } = Guid.NewGuid();

    public virtual ProcessedFile? ProcessedFile { get; set; }
}