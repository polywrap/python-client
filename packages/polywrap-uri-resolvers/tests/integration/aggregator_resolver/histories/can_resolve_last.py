EXPECTED = [
  "wrap://test/3 => TestAggregator => uri (wrap://test/4)",
  [
      "wrap://test/3 => Redirect (wrap://test/1 - wrap://test/2)",
      "wrap://test/3 => Redirect (wrap://test/2 - wrap://test/3)",
      "wrap://test/3 => Redirect (wrap://test/3 - wrap://test/4) => uri (wrap://test/4)",
  ]
]
