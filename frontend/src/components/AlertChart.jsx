import React, { useState, useEffect } from "react";
import { LineChart, Line, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer, ReferenceLine } from "recharts";
import axios from "axios";
import { useNavigate, useParams } from 'react-router-dom';

const AlertChart = () => {
  const { alertId } = useParams();  // Get alertId from URL params
  const [alertData, setAlertData] = useState(null);
  const navigate = useNavigate();

  // Normal ECG values (you can fetch this from a database or use the provided array)
  const normalECG = [1.0, 0.7946814894676208, 0.375386506319046, 0.11688311398029327, 0.0, 0.17192330956459043, 0.283858984708786, 0.29375386238098145, 0.3259121775627136, 0.34508347511291504, 0.3617810904979706, 0.3623995184898376, 0.36611008644104, 0.3679653704166412, 0.37414965033531195, 0.3778602480888367, 0.3821892440319061, 0.3846629559993744, 0.3988868296146393, 0.40136054158210754, 0.4180581271648407, 0.4434137344360352, 0.4576376080513, 0.48794063925743103, 0.5207173824310303, 0.5596784353256226, 0.604205310344696, 0.6345083713531494, 0.6536796689033508, 0.6728509664535521, 0.6784168481826782, 0.6604823470115662, 0.6215213537216187, 0.5559678673744202, 0.48237475752830505, 0.4384663105010986, 0.3784786760807037, 0.3512677848339081, 0.31972789764404297, 0.3067408800125122, 0.29560914635658264, 0.2931354343891144, 0.29189857840538025, 0.29251700639724726, 0.2789115607738495, 0.2789115607738495, 0.2807668447494507, 0.2807668447494507, 0.2857142984867096, 0.27458256483078, 0.2752009928226471, 0.27396413683891296, 0.2844774127006531, 0.2764378488063812, 0.2752009928226471, 0.2776747047901153, 0.2795299887657165, 0.2826221287250519, 0.2795299887657165, 0.2733457088470459, 0.268398255109787, 0.26901668310165405, 0.2677798271179199, 0.2572665512561798, 0.2523190975189209, 0.252937525510788, 0.2572665512561798, 0.24984538555145264, 0.2510822415351868, 0.2510822415351868, 0.24984538555145264, 0.2418058067560196, 0.24118737876415247, 0.243661105632782, 0.24489796161651609, 0.23933209478855133, 0.2418058067560196, 0.23871366679668424, 0.24242424964904785, 0.24118737876415247, 0.2306740880012512, 0.2325293719768524, 0.22820037603378293, 0.2374768108129501, 0.2430426776409149, 0.243661105632782, 0.2430426776409149, 0.26901668310165405, 0.26345083117485046, 0.29066172242164606, 0.2764378488063812, 0.2782931327819824, 0.25170066952705383, 0.25664812326431274, 0.2523190975189209, 0.24613481760025024, 0.24675324559211728, 0.2380952388048172, 0.22077922523021695, 0.2306740880012512, 0.2356215268373489, 0.24613481760025024, 0.24427953362464905, 0.2504638135433197, 0.25850340723991394, 0.2560296952724457, 0.3469387888908386, 0.41682127118110657, 0.5170068144798279, 0.8695114254951477, 0.9845392704010008, 0.5553494095802307, 0.2418058067560196, 0.030921459197998047, 0.044526901096105576, 0.2275819480419159, 0.268398255109787, 0.2813852727413177, 0.31663575768470764, 0.3259121775627136, 0.3314780592918396, 0.33951762318611145, 0.3487940728664398, 0.3469387888908386, 0.344465047121048, 0.35003092885017395, 0.35930734872818, 0.3667285144329071, 0.37662336230278015, 0.38589981198310846, 0.3976499736309052, 0.41682127118110657, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0, 0.0];

  // Fetch alert data based on the provided alert ID
  useEffect(() => {
    const fetchAlertData = async () => {
      try {
        const response = await axios.get(`/api/alerts/${alertId}`);
        const data = response.data;
        const parsedValues = JSON.parse(data.values); // Parse the JSON string from 'values' field
        setAlertData(parsedValues);
      } catch (error) {
        console.error("Error fetching alert data:", error);
      }
    };

    if (alertId) {
      fetchAlertData();  
    }
  }, [alertId]);

  if (!alertData) {
    return <div>Loading...</div>;
  }


  const chartData = alertData[0].map((value, index) => ({
    time: index + 1,  // X-Axis as time (1, 2, 3, ...)
    abnormal: value, // Abnormal data
    normal: normalECG[index], // Normal data
  }));

  // PQRST wave positions in time (these are just typical values, adjust if needed)
  const pWave = 32;  // Time index for P wave
  const qWave = 99;  // Time index for Q wave
  const rWave = 110;  // Time index for R wave
  const sWave = 122;  // Time index for S wave
  const tWave = 158; // Time index for T wave

  return (

    
      <div>
        <button
        onClick={() => navigate(-1)}
        className="top-4 left-8 px-4 py-2 bg-blue-500 text-white rounded hover:bg-blue-600"
      >
        Go Back
      </button>
        <h1 className="font-bold text-3xl mb-2">Alert ID : 5</h1>

      <ResponsiveContainer width="100%" height={400}>
      <LineChart data={chartData}>
        <CartesianGrid strokeDasharray="3 3" />
        <XAxis dataKey="time" />
        <YAxis />
        <Tooltip />
        <Legend />
        <Line type="monotone" dataKey="abnormal" stroke="#8884d8"  />
        <Line type="monotone" dataKey="normal" stroke="#82ca9d" />

        {/* PQRST Reference lines */}
        <ReferenceLine x={pWave} stroke="blue" label="P" />
        <ReferenceLine x={qWave} stroke="green" label="Q" />
        <ReferenceLine x={rWave} stroke="red" label="R" />
        <ReferenceLine x={sWave} stroke="purple" label="S" />
        <ReferenceLine x={tWave} stroke="orange" label="T" />
      </LineChart>
      
      
    </ResponsiveContainer>
    </div>
  );
};

export default AlertChart;
