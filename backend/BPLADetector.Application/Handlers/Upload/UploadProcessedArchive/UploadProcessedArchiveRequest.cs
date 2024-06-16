using MediatR;

namespace BPLADetector.Application.Handlers.Upload.UploadProcessedArchive;

public sealed record UploadProcessedArchiveRequest(string Link, string Txt, Guid CorrelationId, long  ProcessedMilliseconds) : IRequest;