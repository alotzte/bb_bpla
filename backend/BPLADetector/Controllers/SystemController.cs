using System.Text.Json;
using BPLADetector.Infrastructure.Extensions;
using BPLADetector.Services;
using Microsoft.AspNetCore.Mvc;

namespace BPLADetector.Controllers;

[ApiController]
[Route("/api/system")]
public class SystemController : ControllerBase
{
    private readonly MinIOS3 _minIOService;
    private readonly ILogger<SystemController> _logger;

    public SystemController(MinIOS3 minIoService, ILogger<SystemController> logger)
    {
        _minIOService = minIoService;
        _logger = logger;
    }

    [HttpGet]
    public async Task<ActionResult> ListObjects(CancellationToken cancellationToken = default)
    {
        var responseObjects = await _minIOService.ListObjectsV2(cancellationToken);

        _logger.LogInformation(string.Join("\n===\n",
            responseObjects.Select(s3Object => JsonSerializer.Serialize(s3Object))));

        return Ok();
    }

    [HttpPost("put")]
    public async Task<ActionResult> PutObject(IFormFileCollection files, CancellationToken cancellationToken)
    {
        var uploadFiles = files.Select(fileForm => fileForm.ToUploadFileItem()).ToList();

        var uploadedFiles = await _minIOService.PutObjectsAsync(uploadFiles, cancellationToken);

        return Ok(uploadedFiles);
    }

    [HttpGet("presignedUrl")]
    public async Task<ActionResult> GetPresignedUrl([FromQuery] string key)
    {
        var presignedUrl = await _minIOService.GetPresignedUrlAsync(key, DateTime.Now.AddDays(14));

        return Ok(presignedUrl);
    }

    // [HttpPost("multipart")]
    // public async Task<ActionResult> UploadMultipart(IFormFile file, CancellationToken cancellationToken)
    // {
    //     _logger.LogInformation($"File: {file.FileName}. Length: {file.Length}");
    //     await _s3Service.MultiPartUploadAsync(file.FileName, file.OpenReadStream(), cancellationToken);
    //
    //     _logger.LogInformation(
    //         $"File {file.FileName} successfully uploaded.");
    //
    //     return Ok();
    // }
}