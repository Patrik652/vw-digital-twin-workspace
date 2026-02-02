data "aws_iam_policy_document" "iot" {
  statement {
    effect = "Allow"
    actions = [
      "iot:Connect",
      "iot:Publish",
      "iot:Subscribe",
      "iot:Receive"
    ]
    resources = ["*"]
  }
}
