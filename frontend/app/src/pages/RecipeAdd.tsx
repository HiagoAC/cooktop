import { Button, Card } from 'react-bootstrap';
import { RecipeForm } from '../components/RecipeForm';
import '../styles/RecipeAdd.css';


export function RecipeAdd() {
    return (
        <div className="card-container">
            <Card className="my-2 custom-card">
                <Card.Header className="d-flex justify-content-center">
                    <Card.Title>Add a New Recipe</Card.Title>
                </Card.Header>
                <Card.Body>
                    <RecipeForm />
                </Card.Body>
                <Card.Footer className="d-flex justify-content-center">
                    <Button className="mx-4 custom-button">
                        Add Recipe
                    </Button>
                </Card.Footer>
            </Card>
        </div>
    )
}
