﻿using BPLADetector.Application.Abstractions;
using MediatR;

namespace BPLADetector.Application.Handlers.Results.GetProcessedFiles;

public class GetProcessedFilesHandler : IRequestHandler<GetProcessedFilesRequest, GetFilesPagedResponse>
{
    private readonly IDomainRepository _repository;

    public GetProcessedFilesHandler(IDomainRepository repository)
    {
        _repository = repository;
    }

    public Task<GetFilesPagedResponse> Handle(GetProcessedFilesRequest request, CancellationToken cancellationToken)
    {
        return _repository.GetProcessedFiles(request.Limit, request.Offset, cancellationToken);
    }
}