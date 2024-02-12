import { Card, Col, Image, Row } from 'react-bootstrap';
import { useParams } from 'react-router-dom';
import recipes from '../data/recipe_detail.json';
import '../styles/RecipeDetail.css';
import { RecipeDirectionsCard } from '../components/RecipeDirectionsCard';
import { RecipeIngredientList } from '../components/RecipeIngredientList';
import { RecipeInfoCard } from '../components/RecipeInfoCard';

type Params = {
    id: string;
};


export function RecipeDetail() {
    const { id } = useParams<Params>();
    if (!id || !recipes.hasOwnProperty(id)) {
        return <div>Recipe not found</div>
    };
    const recipe = recipes[id];

    return (
        <>
            <Row md={2} xs={1} className="d-flex align-items-center g-2 mt-2">
                <Col className="image-container">
                    <Image
                        src={recipe.image}
                        alt={recipe.title}
                        className="image"
                        rounded
                    />
                </Col>
                <Col>
                    <RecipeInfoCard {...recipe}/>
                </Col>
            </Row>
            <Row md={2} xs={1} className="align-top g-2 mt-2">
                <Col md={4}>
                    <RecipeIngredientList ingredients={recipe.ingredients}/>
                    <Card className="p-3 mt-2">
                        <Card.Title>Notes</Card.Title>
                        <Card.Body>{recipe.notes}</Card.Body>
                    </Card>
                </Col>
                <Col md={8}>
                    <RecipeDirectionsCard directions={recipe.directions}/>
                </Col>
            </Row>
        </>
    )   
}
