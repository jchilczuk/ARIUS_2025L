import React, { useState, useEffect } from "react";
import { CerealList } from "../CerealList";
import { FilterBar } from "../FilterBar";

const loadJSON = (key) => key && JSON.parse(localStorage.getItem(key));
const saveJSON = (key, data) => localStorage.setItem(key, JSON.stringify(data));

export function Agridata({ memberStateCode }) {
  const [data, setData] = useState(loadJSON(`memberStateCode:${memberStateCode}`) || []);
  const [filter, setFilter] = useState({
    productName: "",
    beginDate: "",
    endDate: "",
  });

  useEffect(() => {
    if (!memberStateCode) return;

    const cached = loadJSON(`memberStateCode:${memberStateCode}`);
    if (cached) {
      setData(cached);
      console.log("Dane załadowane z localStorage:", cached);
    } else {
      const fetchData = async () => {
        try {
          const response = await fetch(`/agrifood/api/cereal/prices?memberStateCodes=${memberStateCode}&beginDate=31/12/2019`);
          const json = await response.json();
          console.log("Dane pobrane z API:", json);

          if (Array.isArray(json)) {
            const cleanedData = json.map(({ memberStateName, productName, referencePeriod, price }) => ({
              memberStateName,
              productName,
              referencePeriod,
              price,
            }));
            setData(cleanedData);
            saveJSON(`memberStateCode:${memberStateCode}`, cleanedData);
            console.log("Dane zapisane do localStorage:", cleanedData);

          } else {
            console.error("Niepoprawna odpowiedź z API", json);
          }
        } catch (error) {
          console.error("Błąd podczas pobierania danych:", error);
        }
      };

      fetchData();
    }
  }, [memberStateCode]);

  const filteredData =
    data?.filter((item) => {
      const parts = item.referencePeriod?.split("/");
      if (!parts || parts.length !== 3) return false;

      const itemDate = new Date(`${parts[2]}-${parts[1]}-${parts[0]}`);
      if (isNaN(itemDate)) return false;

      const nameMatch =
        filter.productName === "" || item.productName === filter.productName;
      const beginMatch = !filter.beginDate || itemDate >= new Date(filter.beginDate);
      const endMatch = !filter.endDate || itemDate <= new Date(filter.endDate);

      return nameMatch && beginMatch && endMatch;
    }) || [];

  const productOptions = Array.from(
    new Set(data?.map((item) => item.productName).filter(Boolean))
  ).sort();

  const numericPrices = filteredData
    .map((item) => parseFloat(item.price?.replace("€", "").replace(",", ".")))
    .filter((val) => !isNaN(val));

  const avgPrice =
    numericPrices.length
      ? (numericPrices.reduce((a, b) => a + b, 0) / numericPrices.length).toFixed(2)
      : null;

  if (!data) return <p>Loading...</p>;
  const memberStateName = data[0]?.memberStateName || memberStateCode;

  return (
    <div>
      <h2 style={{ fontSize: "2em", color: "#2a5d9f", textAlign: "center" }}>
        Cereal market prices in {memberStateName} from 2020
      </h2>
      <FilterBar
        filter={filter}
        onChange={setFilter}
        productOptions={productOptions}
      />
      {avgPrice && (
        <p>
          Mean price for selected time range:{" "}
          <strong style={{ fontSize: "1.5em", color: "#2a5d9f" }}>
            {avgPrice} €/t
          </strong>
        </p>
      )}

      <CerealList items={filteredData} />
    </div>
  );
}
