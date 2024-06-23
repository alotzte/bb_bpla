using BPLADetector.Application.Abstractions;
using MediatR;

namespace BPLADetector.Application.Handlers.Results.GetProcessedFiles;

public class GetProcessedFilesHandler : IRequestHandler<GetProcessedFilesRequest, GetFilesPagedResponse>
{
    private readonly IDomainRepository _repository;

    public GetProcessedFilesHandler(IDomainRepository repository)
    {
        _repository = repository;
    }

    public async Task<GetFilesPagedResponse> Handle(GetProcessedFilesRequest request,
        CancellationToken cancellationToken)
    {
        var files = await _repository.GetProcessedFiles(request.Limit, request.Offset, cancellationToken);

        foreach (var file in files.Items)
        {
            file.UploadDateTime = file.UploadDateTime?.ToLocalTime();
        }

        return files;
    }
}