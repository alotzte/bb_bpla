using MediatR;

namespace BPLADetector.Application.Handlers.File.GetProcessedFile;

public sealed record GetProcessedFileRequest(Guid Id) : IRequest<GetProcessedFileResponse?>;