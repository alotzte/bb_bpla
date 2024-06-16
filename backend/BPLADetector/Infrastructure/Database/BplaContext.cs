using System.Reflection;
using BPLADetector.Domain.Model;
using Microsoft.EntityFrameworkCore;

namespace BPLADetector.Infrastructure.Database;

public class BplaContext : DbContext
{
    public DbSet<UploadedFile> UploadedFiles { get; set; }
    public DbSet<ProcessedFile> ProcessedFiles { get; set; }

    public BplaContext(DbContextOptions<BplaContext> options) : base(options)
    {
    }

    protected override void OnModelCreating(ModelBuilder modelBuilder)
    {
        modelBuilder.ApplyConfigurationsFromAssembly(Assembly.GetExecutingAssembly());
    }

    protected override void OnConfiguring(DbContextOptionsBuilder optionsBuilder)
    {
        optionsBuilder.UseNpgsql();
    }
}