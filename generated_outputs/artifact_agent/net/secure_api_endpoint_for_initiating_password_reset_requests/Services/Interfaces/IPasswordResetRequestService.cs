using SecureApiEndpoint.Models.Requests;
using SecureApiEndpoint.Models.Responses;

namespace SecureApiEndpoint.Services.Interfaces;

public interface IPasswordResetRequestService
{
    Task<PasswordResetRequestResponse> CreatePasswordResetRequestAsync(PasswordResetRequestCreateRequest request);
}