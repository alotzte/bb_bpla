using BPLADetector.Application.Abstractions;
using BPLADetector.Domain.Enums;
using BPLADetector.Domain.Model;
using MediatR;
using Microsoft.Extensions.Logging;

namespace BPLADetector.Application.Handlers.Upload.UploadFile;

public class UploadFileHandler : IRequestHandler<UploadFileRequest>
{
    private readonly ILogger<UploadFileHandler> _logger;
    private readonly IS3Service _s3Service;
    private readonly IDomainRepository _domainRepository;
    private readonly IMlHttpClient _httpClient;

    public UploadFileHandler(
        ILogger<UploadFileHandler> logger,
        IS3Service s3Service,
        IDomainRepository domainRepository,
        IMlHttpClient httpClient)
    {
        _logger = logger;
        _s3Service = s3Service;
        _domainRepository = domainRepository;
        _httpClient = httpClient;
    }

    public async Task Handle(UploadFileRequest request, CancellationToken cancellationToken)
    {
        var uploadedFileDtos = await _s3Service.PutObjectsAsync(request.Items, cancellationToken);

        var uploadedFiles = uploadedFileDtos
            .Select(dto => new UploadedFile
            {
                Status = dto.Status,
                CorrelationId = dto.CorrelationId,
                Filename = dto.Filename,
                Uri = dto.Uri,
                Type = dto.Type,
                UploadDatetime = dto.UploadDatetime
            })
            .ToList();

        _domainRepository.AddRange(uploadedFiles);
        await _domainRepository.SaveChangesAsync(cancellationToken);

        var itemGroups = uploadedFileDtos
            .GroupBy(file => file.Type);

        var uploadedPhotoItems = uploadedFileDtos
            .Where(file => file.Type == FileType.Image)
            .Select(file => new MlPhotoRequestItem
            {
                Url = file.OriginalPresignedUrl,
                CorrelationId = file.CorrelationId
            })
            .ToList();

        var addedProcessedPhotos = new List<ProcessedFile>();
        if (uploadedPhotoItems.Any())
        {
            var processedPhotos = await _httpClient.UploadPhotosAsync(uploadedPhotoItems, cancellationToken);

            var processedUCorrelationIds = processedPhotos.PredictedData.Select(photo => photo.CorrelationId).ToList();

            var processedUploadedPhotos = await _domainRepository
                .GetUploadedFilesByCorrelationId(processedUCorrelationIds, cancellationToken);

            foreach (var uploadedPhoto in processedUploadedPhotos)
            {
                uploadedPhoto.Status = UploadStatus.Ready;
            }

            addedProcessedPhotos = processedPhotos.PredictedData
                .Select(photo => new ProcessedFile
                {
                    Type = FileType.Image,
                    Marks = null,
                    TxtUrl = photo.TxtPath,
                    CorrelationId = photo.CorrelationId,
                    Uri = photo.Link,
                    Filename = Path.GetFileName(photo.Link)
                })
                .ToList();
        }

        var uploadedVideos = uploadedFileDtos
            .Where(file => file.Type == FileType.Video)
            .ToList();

        if (uploadedVideos.Any())
        {
            await _httpClient.UploadVideosAsync(
                uploadedVideos.Select(video => video.OriginalPresignedUrl),
                uploadedVideos.First().CorrelationId,
                cancellationToken);
        }

        if (itemGroups.Any(group => group.Key == FileType.Archive))
        {
            var archive = itemGroups.Single(group => group.Key == FileType.Archive).Single();

            await _httpClient.UploadArchiveAsync(archive.OriginalPresignedUrl, archive.CorrelationId, cancellationToken);
        }

        _domainRepository.AddRange(addedProcessedPhotos);
        await _domainRepository.SaveChangesAsync(cancellationToken);
    }
}