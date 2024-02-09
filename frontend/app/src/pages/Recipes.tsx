import { Row, Col } from 'react-bootstrap';
import recipes from '../data/recipes.json';
import { RecipeInList } from '../components/RecipeInList';

export function Recipes() {
    return (
        <>
            <h1>Recipes</h1>
            <Row lg={3} md={2} xs={1} className="g-4">
                {recipes.map(recipe => (
                    <Col key={recipe.id}><RecipeInList {...recipe} /></Col>
                ))}
            </Row>
        </>
    )
}
