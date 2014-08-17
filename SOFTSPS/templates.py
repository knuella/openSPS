#!/usr/bin/python
    
    for k in range(0, 2):
        for i in range(1, 5):
            inputs.save(
                {
                    "name": "Relay" + (str)(i + 4*k) + "_RM",
                    "shortdsc": "Rückmeldung vom Relay.",
                    "longdsc": "...",
                    "type": "binary input",
                    "path": '~/openSPS/SOFTSPS/output.py',
                    "params":
                        {
                            "safety_value": 0,
                            "hardware_type": "none",
                            "hardware_data": 
                                {
                                    "active_text": "Ein",
                                    "inactive_text": "Aus",
                                }
                        }
                }
            )
    
    for i in range(0, 4):
        inputs.save(
            {
                "name": "Dac" + (str)(i + 1) + "_RM",
                "shortdsc": "Rückmessung vom Dac, also ein ADC ;).",
                "longdsc": "analog-digital-converter",
                "type": "analog input",
                "path": '~/openSPS/SOFTSPS/output.py',
                "params":
                    {
                        "safety_value": 0,
                        "hardware_type": "none",
                        "hardware_data": 
                            {
                                "scaling_type": "LinearScaler",
                                "scaling_data": 
                                    {
                                        "y1":2900,
                                        "y2":0,
                                        "x1":10,
                                        "x2":0
                                    }
                            }
                    }
            }
        )


def the_data_at_runtime():
    """ Testfunction.
    Show the structure of the data in a datapoint at runtime.
    """

    output_dp = {
        "safety_value": 
            {
                "value": 0,
                "exclusive": "gui"
            },
        "actual_value": 
            {
                "value": 0,
                "exclusive": False
            },
        "manual_override": 
            {
                "value": 0,
                "exclusive": "gui"
            },
        "manual_value": 
            {
                "value": 0,
                "exclusive": "gui"
            },
        "state": "don't know",
    }


# create the config in the database
# =================================
add_my_dp_config()
