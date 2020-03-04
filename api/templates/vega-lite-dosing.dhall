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
    , { mapKey = "description", mapValue = json.string "Dosing data" }
    , { mapKey = "height", mapValue = json.string "container" }
    , { mapKey = "layer"
      , mapValue =
          json.array
            [ json.object
                [ { mapKey = "encoding"
                  , mapValue =
                      json.object
                        [ { mapKey = "x"
                          , mapValue =
                              json.object
                                [ { mapKey = "field"
                                  , mapValue = json.string "x"
                                  }
                                , { mapKey = "type"
                                  , mapValue = json.string "quantitative"
                                  }
                                ]
                          }
                        , { mapKey = "y"
                          , mapValue =
                              json.object
                                [ { mapKey = "field"
                                  , mapValue = json.string "y"
                                  }
                                , { mapKey = "type"
                                  , mapValue = json.string "quantitative"
                                  }
                                ]
                          }
                        ]
                  }
                , { mapKey = "mark"
                  , mapValue =
                      json.object
                        [ { mapKey = "opacity", mapValue = json.double 0.5 }
                        , { mapKey = "type", mapValue = json.string "area" }
                        ]
                  }
                ]
            , json.object
                [ { mapKey = "encoding"
                  , mapValue =
                      json.object
                        [ { mapKey = "x"
                          , mapValue =
                              json.object
                                [ { mapKey = "field"
                                  , mapValue = json.string "x"
                                  }
                                , { mapKey = "type"
                                  , mapValue = json.string "quantitative"
                                  }
                                ]
                          }
                        , { mapKey = "y"
                          , mapValue =
                              json.object
                                [ { mapKey = "field"
                                  , mapValue = json.string "y"
                                  }
                                , { mapKey = "type"
                                  , mapValue = json.string "quantitative"
                                  }
                                ]
                          }
                        ]
                  }
                , { mapKey = "mark"
                  , mapValue =
                      json.object
                        [ { mapKey = "strokeJoin"
                          , mapValue = json.string "round"
                          }
                        , { mapKey = "type", mapValue = json.string "line" }
                        ]
                  }
                ]
            , json.object
                [ { mapKey = "layer"
                  , mapValue =
                      json.array
                        [ json.object
                            [ { mapKey = "encoding"
                              , mapValue =
                                  json.object
                                    [ { mapKey = "x"
                                      , mapValue =
                                          json.object
                                            [ { mapKey = "field"
                                              , mapValue = json.string "x"
                                              }
                                            , { mapKey = "type"
                                              , mapValue =
                                                  json.string "quantitative"
                                              }
                                            ]
                                      }
                                    , { mapKey = "y"
                                      , mapValue =
                                          json.object
                                            [ { mapKey = "field"
                                              , mapValue = json.string "y"
                                              }
                                            , { mapKey = "type"
                                              , mapValue =
                                                  json.string "quantitative"
                                              }
                                            ]
                                      }
                                    ]
                              }
                            , { mapKey = "mark"
                              , mapValue =
                                  json.object
                                    [ { mapKey = "filled"
                                      , mapValue = json.bool True
                                      }
                                    , { mapKey = "opacity"
                                      , mapValue = json.integer +1
                                      }
                                    , { mapKey = "tooltip"
                                      , mapValue = json.bool True
                                      }
                                    , { mapKey = "type"
                                      , mapValue = json.string "point"
                                      }
                                    ]
                              }
                            ]
                        ]
                  }
                , { mapKey = "transform"
                  , mapValue =
                      json.array
                        [ json.object
                            [ { mapKey = "filter"
                              , mapValue =
                                  json.string
                                    "datum.x % data('data')[0].frequency === 0 || (datum.x + 1) % data('data')[0].frequency === 0"
                              }
                            ]
                        ]
                  }
                ]
            ]
      }
    , { mapKey = "title", mapValue = json.string "Plot of dosing data" }
    , { mapKey = "transform"
      , mapValue =
          json.array
            [ json.object
                [ { mapKey = "impute", mapValue = json.string "y" }
                , { mapKey = "key", mapValue = json.string "x" }
                , { mapKey = "keyvals"
                  , mapValue =
                      json.object
                        [ { mapKey = "start", mapValue = json.integer +0 }
                        , { mapKey = "step", mapValue = json.integer +1 }
                        , { mapKey = "stop", mapValue = json.double 40.1 }
                        ]
                  }
                ]
            , json.object
                [ { mapKey = "as", mapValue = json.string "y" }
                , { mapKey = "calculate"
                  , mapValue =
                      json.string
                        "data('data')[0].dose * exp(-data('data')[0].kel * (datum.x % data('data')[0].frequency)) + floor(datum.x / data('data')[0].frequency) * data('data')[0].dose * exp(-data('data')[0].kel * (data('data')[0].frequency))"
                  }
                ]
            ]
      }
    , { mapKey = "width", mapValue = json.string "container" }
    ]
