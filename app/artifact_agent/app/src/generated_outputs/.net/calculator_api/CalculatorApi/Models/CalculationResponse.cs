namespace CalculatorApi.Models;

public class CalculationResponse
{
    public string Id { get; set; }
    public double Operand1 { get; set; }
    public double Operand2 { get; set; }
    public string Operation { get; set; }
    public double Result { get; set; }
    public DateTime CreatedAt { get; set; }
    public DateTime UpdatedAt { get; set; }
}