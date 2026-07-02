using Microsoft.AspNetCore.Authorization;
using Microsoft.AspNetCore.Mvc;
using SecureApiEndpoint.Models.Requests;
using SecureApiEndpoint.Models.Responses;
using SecureApiEndpoint.Services.Interfaces;

namespace SecureApiEndpoint.Controllers;

[ApiController]
[Route("api/[controller]")]
[Authorize]
public class PasswordResetRequestController : ControllerBase
{
    private readonly IPasswordResetRequestService _passwordResetRequestService;

    public PasswordResetRequestController(IPasswordResetRequestService passwordResetRequestService)
    {
        _passwordResetRequestService = passwordResetRequestService;
    }

    [HttpPost("password-reset-requests")]
    public async Task<IActionResult> CreatePasswordResetRequest([FromBody] PasswordResetRequestCreateRequest request)
    {
        try
        {
            var response = await _passwordResetRequestService.CreatePasswordResetRequestAsync(request);
            return CreatedAtAction(nameof(CreatePasswordResetRequest), response);
        }
        catch (ArgumentException ex)
        {
            return BadRequest(new ErrorResponse
            {
                Error = new ErrorResponse.ErrorDetails
                {
                    Code = "BadRequest",
                    Message = ex.Message,
                    Details = new List<string> { ex.Message }
                }
            });
        }
        catch (Exception)
        {
            return StatusCode(500, new ErrorResponse
            {
                Error = new ErrorResponse.ErrorDetails
                {
                    Code = "InternalServerError",
                    Message = "An unexpected error occurred.",
                    Details = new List<string> { "An error occurred while processing your request." }
                }
            });
        }
    }
}