using MediatR;

namespace BPLADetector.Application.Handlers.Results.GetProcessedFiles;

public sealed record GetProcessedFilesRequest(int Limit, int Offset)
    : IRequest<GetProcessedFilesPagedResponse>;