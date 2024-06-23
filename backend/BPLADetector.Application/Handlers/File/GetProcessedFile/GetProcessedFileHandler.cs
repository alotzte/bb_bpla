using BPLADetector.Application.Abstractions;
using MediatR;

namespace BPLADetector.Application.Handlers.File.GetProcessedFile;

public class GetProcessedFileHandler : IRequestHandler<GetProcessedFileRequest, GetProcessedFileResponse?>
{
    private readonly IDomainRepository _domainRepository;

    public GetProcessedFileHandler(IDomainRepository domainRepository)
    {
        _domainRepository = domainRepository;
    }

    public Task<GetProcessedFileResponse?> Handle(GetProcessedFileRequest request, CancellationToken cancellationToken)
    {
        return _domainRepository.GetProcessedFileByCorrelationId(request.Id, cancellationToken);
    }
}