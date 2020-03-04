  λ(JSON : Type)
→ λ ( json
    : { array : List JSON → JSON
      , bool : Bool → JSON
      , double : Double → JSON
      , integer : Integer → JSON
      , null : JSON
      , object : List { mapKey : Text, mapValue : JSON } → JSON
      , string : Text → JSON
      }
    )
→ json.object
    [ { mapKey = "\$schema"
      , mapValue = json.string "https://vega.github.io/schema/vega-lite/v4.json"
      }
    , { mapKey = "autosize"
      , mapValue =
          json.object [ { mapKey = "resize", mapValue = json.bool True } ]
      }
    , { mapKey = "data"
      , mapValue =
          json.object [ { mapKey = "name", mapValue = json.string "data" } ]
      }
    , { mapKey = "description"
      , mapValue = json.string "Time-series area chart"
      }
    , { mapKey = "encoding"
      , mapValue =
          json.object
            [ { mapKey = "x"
              , mapValue =
                  json.object
                    [ { mapKey = "axis"
                      , mapValue =
                          json.object
                            [ { mapKey = "title"
                              , mapValue = json.string "x axis"
                              }
                            ]
                      }
                    , { mapKey = "field", mapValue = json.string "x" }
                    , { mapKey = "type", mapValue = json.string "quantitative" }
                    ]
              }
            , { mapKey = "y"
              , mapValue =
                  json.object
                    [ { mapKey = "axis"
                      , mapValue =
                          json.object
                            [ { mapKey = "title"
                              , mapValue = json.string "y axis"
                              }
                            ]
                      }
                    , { mapKey = "field", mapValue = json.string "y" }
                    , { mapKey = "type", mapValue = json.string "quantitative" }
                    ]
              }
            ]
      }
    , { mapKey = "height", mapValue = json.string "container" }
    , { mapKey = "mark", mapValue = json.string "area" }
    , { mapKey = "title", mapValue = json.string "Area chart" }
    , { mapKey = "width", mapValue = json.string "container" }
    ]
