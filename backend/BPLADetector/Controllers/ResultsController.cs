using BPLADetector.Application.Handlers.Results.GetProcessedFiles;
using MediatR;
using Microsoft.AspNetCore.Mvc;

namespace BPLADetector.Controllers;

[ApiController]
[Route("/api/v1/results")]
public class ResultsController : ControllerBase
{
    private readonly ILogger<ResultsController> _logger;
    private readonly IMediator _mediator;

    public ResultsController(ILogger<ResultsController> logger, IMediator mediator)
    {
        _logger = logger;
        _mediator = mediator;
    }

    [HttpGet]
    [ProducesResponseType(typeof(GetFilesPagedResponse), StatusCodes.Status200OK)]
    public async Task<ActionResult<GetFilesPagedResponse>> GetProcessedFiles(
        [FromQuery] int limit,
        [FromQuery] int offset,
        CancellationToken cancellationToken)
    {
        _logger.LogInformation(
            "Получен запрос на получение обработанных файлов. Limit = {limit}, Offset = {offset}",
            limit,
            offset);

        var results = await _mediator.Send(new GetProcessedFilesRequest(limit, offset), cancellationToken);

        return Ok(results);
    }
}