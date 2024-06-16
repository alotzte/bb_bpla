using BPLADetector.Application.Abstractions;
using BPLADetector.Domain.Enums;
using BPLADetector.Domain.Model;
using MediatR;

namespace BPLADetector.Application.Handlers.Upload.UploadProcessedArchive;

public class UploadProcessedArchiveHandler : IRequestHandler<UploadProcessedArchiveRequest>
{
    private readonly IDomainRepository _repository;

    public UploadProcessedArchiveHandler(IDomainRepository repository)
    {
        _repository = repository;
    }

    public async Task Handle(UploadProcessedArchiveRequest request, CancellationToken cancellationToken)
    {
        var filename = Path.GetFileName(request.Link);

        var uploadFile = await _repository.GetUploadedFileByCorrelationId(request.CorrelationId, cancellationToken);
        if (uploadFile is not null)
        {
            uploadFile.Status = UploadStatus.Ready;
        }
        
        var addedProcessedArchive = new ProcessedFile
        {
            UploadDatetime = DateTime.UtcNow,
            Type = FileType.Archive,
            Uri = request.Link,
            TxtUrl = request.Txt,
            Filename = filename,
            CorrelationId = request.CorrelationId,
            ProcessedMilliseconds = request.ProcessedMilliseconds
        };

        await _repository.AddAsync(addedProcessedArchive, cancellationToken);
        await _repository.SaveChangesAsync(cancellationToken);
    }
}