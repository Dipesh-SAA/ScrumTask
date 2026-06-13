namespace CalculatorApi.Models;

public class CalculationCreateRequest
{
    public double Operand1 { get; set; }
    public double Operand2 { get; set; }
    public string Operation { get; set; }
}