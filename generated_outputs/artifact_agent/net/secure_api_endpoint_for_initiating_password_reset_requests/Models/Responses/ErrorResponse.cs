namespace SecureApiEndpoint.Models.Responses;

public class ErrorResponse
{
    public ErrorDetails Error { get; set; } = new ErrorDetails();

    public class ErrorDetails
    {
        public string Code { get; set; } = string.Empty;
        public string Message { get; set; } = string.Empty;
        public List<string> Details { get; set; } = new List<string>();
    }
}