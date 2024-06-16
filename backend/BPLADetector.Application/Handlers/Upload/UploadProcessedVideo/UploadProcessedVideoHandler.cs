using BPLADetector.Application.Abstractions;
using BPLADetector.Domain.Enums;
using BPLADetector.Domain.Model;
using MediatR;

namespace BPLADetector.Application.Handlers.Upload.UploadProcessedVideo;

public class UploadProcessedVideoHandler : IRequestHandler<UploadProcessedVideoRequest>
{
    private readonly IDomainRepository _repository;

    public UploadProcessedVideoHandler(IDomainRepository repository)
    {
        _repository = repository;
    }

    public async Task Handle(UploadProcessedVideoRequest request, CancellationToken cancellationToken)
    {
        var filename = Path.GetFileName(request.Link);

        var uploadFile = await _repository.GetUploadedFileByCorrelationId(request.CorrelationId, cancellationToken);
        if (uploadFile is not null)
        {
            uploadFile.Status = UploadStatus.Ready;
        }
        
        uploadFile!.Status = UploadStatus.Ready;
        
        var addedProcessedVideo = new ProcessedFile
        {
            UploadDatetime = DateTime.UtcNow,
            Type = FileType.Video,
            Marks = request.Marks,
            Uri = request.Link,
            Filename = filename,
            CorrelationId = request.CorrelationId,
            ProcessedMilliseconds = request.ProcessedMilliseconds
        };

        await _repository.AddAsync(addedProcessedVideo, cancellationToken);
        await _repository.SaveChangesAsync(cancellationToken);
    }
}