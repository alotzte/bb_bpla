using System.Net.Mime;
using System.Text;
using System.Text.Json;
using BPLADetector.Application.Abstractions;
using BPLADetector.Domain.Model;

namespace BPLADetector.Infrastructure.Http;

public sealed class MlHttpClient : IMlHttpClient, IDisposable
{
    private readonly HttpClient _httpClient;
    private readonly ILogger<MlHttpClient> _logger;

    public MlHttpClient(HttpClient httpClient, ILogger<MlHttpClient> logger)
    {
        _httpClient = httpClient;
        _logger = logger;
    }

    public async Task<MlPhotosResponse?> UploadPhotosAsync(
        IEnumerable<MlPhotoRequestItem> items,
        CancellationToken cancellationToken = default)
    {
        var body = new MlPhotoRequest
        {
            Photos = items.ToArray()
        };

        using var json = new StringContent(
            JsonSerializer.Serialize(body),
            Encoding.UTF8,
            MediaTypeNames.Application.Json);

        _logger.LogInformation($"ML request body: {JsonSerializer.Serialize(json)}");

        using var responseMessage = await _httpClient.PostAsync("/ml/predict_photos", json, cancellationToken);

        try
        {
            responseMessage.EnsureSuccessStatusCode();
        }
        catch (Exception e)
        {
            var responseBody = await responseMessage.Content.ReadAsStringAsync(cancellationToken);
            _logger.LogError(e, "Response body:\n {responseBody} \n", responseBody);
            throw;
        }

        var responseString = await responseMessage.Content.ReadAsStringAsync(cancellationToken);
        return JsonSerializer.Deserialize<MlPhotosResponse>(responseString);
    }

    public async Task UploadVideosAsync(
        IEnumerable<string> urls,
        Guid correlationId,
        CancellationToken cancellationToken = default)
    {
        var body = new MlVideoRequest
        {
            Urls = urls.ToArray()
        };

        using var json = new StringContent(
            JsonSerializer.Serialize(body),
            Encoding.UTF8,
            MediaTypeNames.Application.Json);

        json.Headers.Add("CorrelationId", correlationId.ToString());

        _logger.LogInformation($"ML request body: {json}");

        using var responseMessage = await _httpClient.PostAsync("/ml/predict_video", json, cancellationToken);

        try
        {
            responseMessage.EnsureSuccessStatusCode();
        }
        catch (Exception e)
        {
            var responseBody = await responseMessage.Content.ReadAsStringAsync(cancellationToken);
            _logger.LogError(e, "Response body:\n {responseBody} \n", responseBody);
            throw;
        }
    }

    public async Task UploadArchiveAsync(
        string url,
        Guid correlationId,
        CancellationToken cancellationToken = default)
    {
        var body = new MlArchiveRequest
        {
            Archives = new[]
            {
                new MlArchiveRequest.ArchiveItem
                {
                    Url = url,
                    CorrelationId = correlationId
                }
            }
        };

        using var json = new StringContent(
            JsonSerializer.Serialize(body),
            Encoding.UTF8,
            MediaTypeNames.Application.Json);

        json.Headers.Add("CorrelationId", correlationId.ToString());

        _logger.LogInformation($"ML request body: {json}");

        using var responseMessage = await _httpClient.PostAsync("/ml/predict_photos_archive", json, cancellationToken);

        try
        {
            responseMessage.EnsureSuccessStatusCode();
        }
        catch (Exception e)
        {
            var responseBody = await responseMessage.Content.ReadAsStringAsync(cancellationToken);
            _logger.LogError(e, "Response body:\n {responseBody} \n", responseBody);
            throw;
        }
    }

    public void Dispose()
    {
        _httpClient?.Dispose();
    }
}