using BPLADetector.Application;
using BPLADetector.Application.Abstractions;
using BPLADetector.Configuration;
using BPLADetector.Configuration.Http;
using BPLADetector.Infrastructure.Database;
using BPLADetector.Infrastructure.Http;
using BPLADetector.Infrastructure.Middleware;
using BPLADetector.Services;
using Microsoft.EntityFrameworkCore;
using Serilog;
using Serilog.Events;

Log.Logger = new LoggerConfiguration()
    .Enrich.FromLogContext()
    .MinimumLevel.Verbose()
    .WriteTo.Console(LogEventLevel.Debug)
    .WriteTo.File("log-.txt", rollingInterval: RollingInterval.Day)
    .CreateLogger();


var builder = WebApplication.CreateBuilder(args);
builder.Services.AddSerilog();

builder.Services.AddMediatR(cfg => cfg.RegisterServicesFromAssemblyContaining<ApplicationAssembly>());

builder.Services.AddDbContext<BplaContext>(options =>
    options.UseNpgsql(builder.Configuration.GetConnectionString("BplaContext")));

builder.Services.AddControllers();
builder.Services.AddEndpointsApiExplorer();
builder.Services.AddSwaggerGen();

builder.Services.Configure<CloudOptions>(builder.Configuration.GetSection(CloudOptions.Section));
builder.Services.Configure<DigitalOceanOptions>(builder.Configuration.GetSection(DigitalOceanOptions.Section));
builder.Services.Configure<MinIOOptions>(builder.Configuration.GetSection(MinIOOptions.Section));

builder.Services.Configure<MlHttpOptions>(builder.Configuration.GetSection(MlHttpOptions.Section));

builder.Services.AddCors(options => options.AddPolicy("AllowAll",
    builder => builder.AllowAnyOrigin().AllowAnyHeader().AllowAnyMethod()));

builder.Services.AddHttpClient<IMlHttpClient, MlHttpClient>(client =>
{
    client.BaseAddress =
        new Uri(builder.Configuration[$"{MlHttpOptions.Section}:{nameof(MlHttpOptions.BaseUri)}"]!);
});

builder.Services.AddScoped<IS3Service, DigitalOceanS3>();
builder.Services.AddScoped<MinIOS3>();

builder.Services.AddScoped<IDomainRepository, DomainRepository>();


var app = builder.Build();

app.UseSerilogRequestLogging();

app.UseMiddleware<ExceptionHandlingMiddleware>();

app.UseCors("AllowAll");
app.UseSwagger();
app.UseSwaggerUI();

app.MapControllers();

app.Run();