import React from "react";

export function FilterBar({ filter, onChange, productOptions }) {
  return (
    <div
      style={{
        color: "#2a5d9f",
        marginBottom: "3rem",
        display: "flex",
        gap: "20px",
        flexWrap: "wrap",
        justifyContent: "center", 
        alignItems: "flex-end"
      }}
    >
      <div style={{ display: "flex", flexDirection: "column" }}>
        <label><strong>Product name:</strong></label>
        <select
          className="filter-input"
          value={filter.productName}
          onChange={e => onChange({ ...filter, productName: e.target.value })}
        >
          <option value="">All Products</option>
          {productOptions.map((name, idx) => (
            <option key={idx} value={name}>{name}</option>
          ))}
        </select>
      </div>

      <div style={{ display: "flex", flexDirection: "column" }}>
        <label><strong>From (date):</strong></label>
        <input
          className="filter-input"
          type="date"
          value={filter.beginDate}
          onChange={e => onChange({ ...filter, beginDate: e.target.value })}
        />
      </div>

      <div style={{ display: "flex", flexDirection: "column" }}>
        <label><strong>To (date):</strong></label>
        <input
          className="filter-input"
          type="date"
          value={filter.endDate}
          onChange={e => onChange({ ...filter, endDate: e.target.value })}
        />
      </div>
    </div>
  );
}
