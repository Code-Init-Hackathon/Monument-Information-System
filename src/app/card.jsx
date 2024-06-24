export default function Card({imageUrl,name}){
    return(
        <div className="card">
            <img src={imageUrl} alt={name} className="card-image" />
            <div className="card-name">{name}</div>
        </div>
    );
}