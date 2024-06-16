using MediatR;

namespace BPLADetector.Application.Handlers.File.GetProcessedFile;

public sealed record GetProcessedFileRequest(long Id) : IRequest<GetProcessedFileResponse?>;