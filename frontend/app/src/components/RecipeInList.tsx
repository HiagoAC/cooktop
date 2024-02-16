import { Link } from 'react-router-dom';
import { Card } from 'react-bootstrap';
import { BadgeStack } from './BadgeStack';
import '../styles/RecipeInList.css';
import clockIcon from '../assets/clock_icon.svg';


type Props = {
    id: number,
    title: string,
    time_minutes: number,
    tags: Array<string>,
    image: string
}


export function RecipeInList({ id, title, time_minutes, tags, image }:
    Props) {
        return <Card>
            <Card.Img
                variant="top"
                src={image}
                height="200px"
                className="card-img"
            />
            <Card.Body className="d-flex flex-column" key={id}>
                <Card.Title>{title}</Card.Title>
                <Card.Text>
                    <span>
                        <div className="icon-container">
                            <img
                                src={clockIcon}
                                alt="prep time"
                                className="clock-icon"
                            />
                        </div> {time_minutes} min
                    </span>
                    <BadgeStack items={tags} />
                </Card.Text>
                <Link to={`/recipes/${id.toString()}`} className="stretched-link" />
            </Card.Body>
        </Card>
}