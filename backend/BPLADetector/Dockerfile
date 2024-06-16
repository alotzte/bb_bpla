FROM mcr.microsoft.com/dotnet/aspnet:7.0 AS base
WORKDIR /app
EXPOSE 80
EXPOSE 443

FROM mcr.microsoft.com/dotnet/sdk:7.0 AS build
ARG BUILD_CONFIGURATION=Release
WORKDIR /src
COPY ["BPLADetector/BPLADetector.csproj", "BPLADetector/"]
COPY ["BPLADetector.Application/BPLADetector.Application.csproj", "BPLADetector.Application/"]
COPY ["BPLADetector.Domain/BPLADetector.Domain.csproj", "BPLADetector.Domain/"]
RUN dotnet restore "BPLADetector/BPLADetector.csproj"
COPY . .
WORKDIR "/src/BPLADetector"
RUN dotnet build "BPLADetector.csproj" -c $BUILD_CONFIGURATION -o /app/build

FROM build AS publish
ARG BUILD_CONFIGURATION=Release
RUN dotnet publish "BPLADetector.csproj" -c $BUILD_CONFIGURATION -o /app/publish /p:UseAppHost=false

FROM base AS final
WORKDIR /app
COPY --from=publish /app/publish .
ENTRYPOINT ["dotnet", "./BPLADetector.dll"]
