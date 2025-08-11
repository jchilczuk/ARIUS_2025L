import React from "react";
import { FixedSizeList } from "react-window";

export function CerealList({ items }) {
  const renderRow = ({ index, style }) => {
    const item = items[index];
    
    return (
      <div style={{ ...style, display: "flex", padding: "4px", borderBottom: "1px solid #eee" }}>
        <div style={{ flex: 2 }}>{item.productName}</div>
        <div style={{ flex: 2 }}>{item.referencePeriod}</div>
        <div style={{ flex: 1 }}>{item.price}</div>
      </div>
    );
  };

  if (!items || items.length === 0) return <p>No data to display, please adjust the filters.</p>;
  

  return (
    
    <div>
      <div style={{ display: "flex", fontWeight: "bold", borderBottom: "2px solid #000", padding: "4px", background: "#fff" }}>
        <div style={{ flex: 2 }}>Product Name</div>
        <div style={{ flex: 2 }}>Reference period</div>
        <div style={{ flex: 1 }}>Price</div>
      </div>

      <FixedSizeList
        height={window.innerHeight - 200}
        width={window.innerWidth - 20}
        itemCount={items.length}
        itemSize={40}
      >
        {renderRow}
      </FixedSizeList>
    </div>
  );
}
