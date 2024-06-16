using MediatR;

namespace BPLADetector.Application.Handlers.Upload.UploadProcessedVideo;

public sealed record UploadProcessedVideoRequest(string Link, float[]? Marks, Guid CorrelationId, long  ProcessedMilliseconds) : IRequest;