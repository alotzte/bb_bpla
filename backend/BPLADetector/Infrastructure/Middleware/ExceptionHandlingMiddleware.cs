using System.Net;
using System.Net.Mime;

namespace BPLADetector.Infrastructure.Middleware;

public class ExceptionHandlingMiddleware
{
    private record ExceptionResponse(HttpStatusCode StatusCode);

    private readonly RequestDelegate _next;
    private readonly ILogger<ExceptionHandlingMiddleware> _logger;

    public ExceptionHandlingMiddleware(RequestDelegate next, ILogger<ExceptionHandlingMiddleware> logger)
    {
        _next = next;
        _logger = logger;
    }

    public async Task InvokeAsync(HttpContext httpContext)
    {
        try
        {
            await _next(httpContext);
        }
        catch (Exception exception)
        {
            await HandleExceptionAsync(httpContext, exception);
        }
    }

    private async Task HandleExceptionAsync(HttpContext context, Exception exception)
    {
        _logger.LogError(exception, "Произошла непредвиденная ошибка: ");

        var response = exception switch
        {
            ApplicationException => new ExceptionResponse(HttpStatusCode.BadRequest),
            _ => new ExceptionResponse(HttpStatusCode.InternalServerError)
        };

        context.Response.ContentType = MediaTypeNames.Application.Json;
        context.Response.StatusCode = (int)response.StatusCode;

        await context.Response.WriteAsJsonAsync(response);
    }
}