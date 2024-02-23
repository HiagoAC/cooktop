import { Button } from 'react-bootstrap';
import { PantryIngredient, pantryIngredients} from '../data/pantry';
import '../styles/global.css';


export function Pantry() {
    return (
        <>
            <div className="page-title mt-3">Pantry</div>
            <div className="d-flex justify-content-center mt-2 mb-5">
                <Button className="custom-button">Add new item</Button>
            </div>
            <div>
                {pantryIngredients.map((ingredient: PantryIngredient) => (
                    <div className="mb-2" key={ingredient.id}>{ingredient.name}</div>
                ))}
            </div>
        </>
    )
}
